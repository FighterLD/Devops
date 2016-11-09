#!/bin/bash
#monitor available memory space
#查看内存占用的百分比  free -m | sed -n '2p' | awk '{print "used mem is "$3"M,total mem is "$2"M,used percent is "$3/$2*100"%"}'
#系统分配的内存总量
mem_total=`free -m | grep Mem | awk '{print  $2}'`

#当前剩余的free大小
mem_free=`free -m | grep Mem | awk '{print  $4}'`

#当前已使用的used大小
mem_used=`free -m | grep Mem | awk '{print  $3}'`

#if (($mem_used != 0)); then
#如果已被使用，则计算当前剩余free所占总量的百分比，用小数来表示，要在小数点前面补一个整数位0
  mem_per=0`echo "scale=2;$mem_free/$mem_total" | bc`
  DATA="$(date -d "today" +"%Y-%m-%d-%H-%M") free percent is : $mem_per"

#设置的告警值为10%(即使用超过90%的时候告警)。
  mem_warn=0.10

#当前剩余百分比与告警值进行比较（当大于告警值(即剩余10%以上)时会返回1，小于(即剩余不足10%)时会返回0 ）
  mem_now=`expr $mem_per \> $mem_warn`

echo "mem_total:$mem_total"
echo "mem_free:$mem_free"
echo "mem_used:$mem_used"
echo "mem_now:$mem_now"
##如果当前使用超过80%（即剩余小于10%，上面的返回值等于0），释放内存
#  if (($mem_now == 0)); then
#
#        DAT="`date +%Y%m%d`"
#		HOUR="`date +%H`"
#		DIR="/home/bigdata/logs/host_${DAT}/${HOUR}"
#		DELAY=60
#		COUNT=60
#		# whether the responsible directory exist
#		if ! test -d ${DIR}
#		then
#		    /bin/mkdir -p ${DIR}
#		fi
#		# general check
#		export TERM=linux
#		/usr/bin/top -b -d ${DELAY} -n ${COUNT} > ${DIR}/top_${DAT}.log 2>&1 &
#		# cpu check
#		#/usr/bin/sar -u ${DELAY} ${COUNT} > ${DIR}/cpu_${DAT}.log 2>&1 &
#		#/usr/bin/mpstat -P 0 ${DELAY} ${COUNT} > ${DIR}/cpu_0_${DAT}.log 2>&1 &
#		#/usr/bin/mpstat -P 1 ${DELAY} ${COUNT} > ${DIR}/cpu_1_${DAT}.log 2>&1 &
#		# memory check
#		/usr/bin/vmstat ${DELAY} ${COUNT} > ${DIR}/vmstat_${DAT}.log 2>&1 &
#		# I/O check
#		#/usr/bin/iostat ${DELAY} ${COUNT} > ${DIR}/iostat_${DAT}.log 2>&1 &
#		# network check
#		#/usr/bin/sar -n DEV ${DELAY} ${COUNT} > ${DIR}/net_${DAT}.log 2>&1 &
#		#/usr/bin/sar -n EDEV ${DELAY} ${COUNT} > ${DIR}/net_edev_${DAT}.log 2>&1 &
#                ps -ef|grep python|awk '{print $2}'|xargs kill -9
#                bash /home/bigdata/github/resumeSpider/sh/celery_start_spider.sh &
#  fi
#fi
